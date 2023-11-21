#include <lely/ev/loop.hpp>
#if _WIN32
#include <lely/io2/win32/ixxat.hpp>
#include <lely/io2/win32/poll.hpp>
#elif defined(__linux__)
#include <lely/io2/linux/can.hpp>
#include <lely/io2/posix/poll.hpp>
#else
#error This file requires Windows or Linux.
#endif
#include <lely/io2/sys/io.hpp>
#include <lely/io2/sys/sigset.hpp>
#include <lely/io2/sys/timer.hpp>
#include <lely/coapp/slave.hpp>

#include <iostream>
#include <ctime>
#include <functional>
#include "AntennaSimulate.h"

// Time
#include <thread>
#include <chrono>
#include <atomic>
#include <condition_variable>
#include <mutex>

#if _WIN32
#include <thread>
#endif

using namespace lely;
using namespace std;

const long periodMs = 500;   // See cpp-tutorial.yml sync_period

class MySlave : public canopen::BasicSlave {
 public:
  using BasicSlave::BasicSlave;

 protected:
  // This function gets called every time a value is written to the local object
  // dictionary by an SDO or RPDO.
  void
  OnWrite(uint16_t idx, uint8_t subidx) noexcept override {
    if (idx == 0x4000 && subidx == 0) 
    {
      // Read the value just written to object 4000:00, probably by RPDO 1.
      uint32_t val = (*this)[0x4000][0];
      // Copy it to object 4001:00, so that it will be sent by the next TPDO.
      (*this)[0x4001][0] = val;
    }

    // Mode command
    if (0x2100 == idx)
    { 
      ::std::error_code ec;
      uint32_t modeCmd = this->Get<uint32_t>(0x2100, 1, ec);
      cout << BLUE << "[+] Mode command: " << (int) modeCmd << RESET_COLOR << "\n";
      string modeCmdName = pAntennaSimulate->GetModeCmdName(modeCmd);
      pAntennaSimulate->HandleModeCmd(modeCmdName);
    }
    // Pointing
    if (0x2000 == idx)
    {
      switch (subidx)
      {
        case 1:
          timestamp = (*this)[idx][subidx];
          std::cout << "Rx: " << idx << ":" << (uint16_t ) subidx << " = " <<  timestamp << endl;
          gotTs = true;
          break;
        case 2:
          azimuth = (*this)[idx][subidx];
          std::cout << "Rx: " << idx << ":" << (uint16_t ) subidx << " = " <<  azimuth << endl;
          gotAzi = true;
          break;
        case 3:
          elevation = (*this)[idx][subidx];
          std::cout << "Rx: " << idx << ":" << (uint16_t ) subidx << " = " <<  elevation << endl;
          gotEle = true;
          break;
      }
      if (gotTs && gotAzi && gotEle)
      {
        gotTs = false;
        gotAzi = false;
        gotEle = false;
        pAntennaSimulate->RequestPosition(timestamp, azimuth, elevation);
      }
    }
  }
  public:
    void StartSyncChecking()
    {
      run = true;
      chkOnSyncThread = thread(&MySlave::CheckOnSync, this);
    }
    ~MySlave()
    {
      run = false;
      chkOnSyncThread.join();
    }
  // PJP
  // Function invoked when a SYNC message is sent/received
    void OnSyncFunc([[maybe_unused]] uint8_t cnt, const time_point &tp)
    {
      // Got sync - notify thread checking the onsync
      cv.notify_one();
      static time_point prevTp; // std::chrono::steady_clock::now();

      //cout << "[+] OnSync " << cnt << " " << (tp - prevTp)/1ms  << "\n";
      prevTp = tp;

      // Run state machines
      if (pAntennaSimulate->ApplicationStateMachine())
      {
        // Update feedback
        // Application state
        uint8_t appState = pAntennaSimulate->GetApplicationState();
        //this->Set<uint8_t>(0x2101, 1, appState);
        (*this)[0x2101][1] = appState;
        cout << CYAN << "[+] Application State change = " << (int ) appState << "\n";
      }
      if (pAntennaSimulate->FunctionalStateMachine())
      {
        // Update feedback
        // Functional state
        uint8_t funcState = pAntennaSimulate->GetFunctionalState();
        //this->Set<uint8_t>(0x2101, 2, funcState);
        (*this)[0x2101][2] = funcState; 
        cout << CYAN << "[+] Functional State change = " << (int ) funcState << "\n";
      }
      if (pAntennaSimulate->ModeStateMachine())
      {
        // Update feedback
        // Mode
        uint8_t mode = pAntennaSimulate->GetMode();
        //this->Set<uint8_t>(0x2101, 3, mode);
        (*this)[0x2101][3] = mode;
        cout << CYAN << "[+] Mode change = " << (int ) mode << "\n";
      }

      pAntennaSimulate->ControlSpeed();
      tuple<double, double, double> actualPos = pAntennaSimulate->SimulatePosition();
      (*this)[0x2001][1] = get<0>(actualPos);
      (*this)[0x2001][2] = get<1>(actualPos);
      (*this)[0x2001][3] = get<2>(actualPos);
      pAntennaSimulate->SimulateStowWindow();
      DigitalInputs dInputs = pAntennaSimulate->GetDInputs();
      (*this)[0x2200][1] = (uint8_t) dInputs.raw;
    }	
   
  public:
    static AntennaSimulate *pAntennaSimulate;
  private:
    bool gotTs = false;
    bool gotAzi = false;
    bool gotEle = false;
    double timestamp;
    double azimuth;
    double elevation;
    // Check OnSync
    condition_variable cv;
    mutex cvMutex;
    thread chkOnSyncThread;
    atomic<bool> run;

  private:
    void CheckOnSync()
    {
      while (run)
      {
        std::unique_lock<mutex> lock(cvMutex);
        if (std::cv_status::timeout == cv.wait_for(lock, chrono::milliseconds(2*periodMs)))
        {
          // Sync did not occur
          cerr << RED << "[-] Sync did not occur within " << 2*periodMs << " ms" << RESET_COLOR << "\n";
          pAntennaSimulate->SetMode(0); // Set mode to idle
        }
      }
    } 
};

AntennaSimulate *MySlave::pAntennaSimulate;

int
main() 
{
  // Create antenna simulate
  AntennaSimulate antennaSimulate(periodMs);

  // Initialize the I/O library. This is required on Windows, but a no-op on
  // Linux (for now).
  io::IoGuard io_guard;
#if _WIN32
  // Load vcinpl2.dll (or vcinpl.dll if CAN FD is disabled).
  io::IxxatGuard ixxat_guard;
#endif
  // Create an I/O context to synchronize I/O services during shutdown.
  io::Context ctx;
  // Create an platform-specific I/O polling instance to monitor the CAN bus, as
  // well as timers and signals.
  io::Poll poll(ctx);
  // Create a polling event loop and pass it the platform-independent polling
  // interface. If no tasks are pending, the event loop will poll for I/O
  // events.
  ev::Loop loop(poll.get_poll());
  // I/O devices only need access to the executor interface of the event loop.
  auto exec = loop.get_executor();
  
  // Create a timer using a monotonic clock, i.e., a clock that is not affected
  // by discontinuous jumps in the system time.
  io::Timer timer(poll, exec, CLOCK_MONOTONIC);  
#if _WIN32
  // Create an IXXAT CAN controller and channel. The VCI requires us to
  // explicitly specify the bitrate and restart the controller.
  io::IxxatController ctrl(0, 0, io::CanBusFlag::NONE, 125000);
  ctrl.restart();
  io::IxxatChannel chan(ctx, exec);
#elif defined(__linux__)
  // Create a virtual SocketCAN CAN controller and channel, and do not modify
  // the current CAN bus state or bitrate.
// PJP  io::CanController ctrl("vcan0");
  io::CanController ctrl("can0");
  io::CanChannel chan(poll, exec);
#endif
  chan.open(ctrl);

  // Create a CANopen slave with node-ID 2.
  MySlave slave(timer, chan, "cpp-slave.eds", "", 2);
  slave.StartSyncChecking();

  // Setup callback
  MySlave::pAntennaSimulate = &antennaSimulate;
  using namespace std::placeholders;
  using SyncFunction = function<void(uint8_t cnt, const lely::canopen::Node::time_point)>;
  SyncFunction f = std::bind(&MySlave::OnSyncFunc, &slave, _1, _2);
  slave.OnSync(f);
 
  // Create a signal handler.
  io::SignalSet sigset(poll, exec);
  // Watch for Ctrl+C or process termination.
  sigset.insert(SIGHUP);
  sigset.insert(SIGINT);
  sigset.insert(SIGTERM);

  // Submit a task to be executed when a signal is raised. We don't care which.
  sigset.submit_wait([&](int /*signo*/) 
  {
    // If the signal is raised again, terminate immediately.
    sigset.clear();
    // Perform a clean shutdown.
    ctx.shutdown();
  });

  // Start the NMT service of the slave by pretending to receive a 'reset node'
  // command.
  slave.Reset();

#if _WIN32
  // Create two worker threads to ensure the blocking canChannelReadMessage()
  // and canChannelSendMessage() used by the IXXAT CAN channel do not hold up
  // the event loop.
  std::thread workers[] = {std::thread([&]() { loop.run(); }),
                           std::thread([&]() { loop.run(); })};
#endif

  // Run the event loop until no tasks remain (or the I/O context is shut down).
  loop.run();

#if _WIN32
  // Wait for the worker threads to finish.
  for (auto& worker : workers) worker.join();
#endif

  return 0;
}
