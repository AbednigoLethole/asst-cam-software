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

  function addAzimuthData(label, data) {
    myChart.data.labels.push(label);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart.update();
  }

  function removeFirstAzimuthData() {
    myChart.data.labels.splice(0, 1);
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  function addElevationData(label, data) {
    myChart2.data.labels.push(label);
    myChart2.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    myChart2.update();
  }

  function removeFirstElevationData() {
    myChart2.data.labels.splice(0, 1);
    myChart2.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 30;
  //const MAX_DATA_COUNT2 = 30;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive azimuth from server.
  socket.on("updateAZELData", function (msg) {
    console.log("Received elevation Data :: " + msg.date + " :: " + msg.az+ " :: "+ msg.el);

    // Show only MAX_DATA_COUNT data
    if (myChart.data.labels.length && myChart2.data.labels.length > MAX_DATA_COUNT) {
      removeFirstAzimuthData();
      removeFirstElevationData();

    }
    addAzimuthData(msg.date, msg.az);
    addElevationData(msg.date, msg.el);
  });

});
