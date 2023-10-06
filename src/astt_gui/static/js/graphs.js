$(document).ready(function () {
    const ctx = document.getElementById("myChart").getContext("2d");
    const ctx2 = document.getElementById("myChart2").getContext("2d");
  
    const myChart = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [{ label: "Azimuth",  }],
      },
      options: {
        borderWidth: 3,
        borderColor: ['rgba(255, 99, 132, 1)',],
      },
    });

    //Second graph
    const myChart2 = new Chart(ctx2, {
        type: "line",
        data: {
          datasets: [{ label: "Elevation",  }],
        },
        options: {
          borderWidth: 3,
          borderColor: ['rgba(255, 99, 132, 1)',],
        },
      });
  
    function addData(label, data) {
      myChart.data.labels.push(label);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
      myChart.update();
    }

    function addData(label, data) {
        myChart2.data.labels.push(label);
        myChart2.data.datasets.forEach((dataset) => {
          dataset.data.push(data);
        });
        myChart2.update();
      }
  
    function removeFirstData() {
      myChart.data.labels.splice(0, 1);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
      });
    }

    function removeFirstData() {
        myChart2.data.labels.splice(0, 1);
        myChart2.data.datasets.forEach((dataset) => {
          dataset.data.shift();
        });
      }
  
    const MAX_DATA_COUNT = 10;
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
    var socket = io.connect();
  
    //receive details from server
    socket.on("updateSensorData", function (msg) {
      console.log("Received sensorData :: " + msg.date + " :: " + msg.value);
  
      // Show only MAX_DATA_COUNT data
      if (myChart.data.labels.length && myChart2.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
      }
      addData(msg.date, msg.value);
    });
  });