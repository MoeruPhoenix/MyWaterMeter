FusionCharts.ready(function() {
  var chart = new FusionCharts({
      type: 'hled',
      renderAt: 'chart-container',
      width: '360',
      height: '200',
      dataFormat: 'json',
      dataSource: {
        "chart": {
          "lowerLimit": "0",
          "upperLimit": "14",
          "lowerLimitDisplay": "1",
          "upperLimitDisplay": "14",
          //"numberSuffix": "",
          "valueFontSize": "12",
          //hover effect
          "showhovereffect": "1",

          "theme": "fusion",
          "ledSize": "1"
        },
        "colorRange": {
          "color": [{
            "minValue": "0",
            "maxValue": "1",
            "code": "#ed1f27"
          }, {
            "minValue": "1",
            "maxValue": "2",
            "code": "#ee7821"
          }, {
            "minValue": "2",
            "maxValue": "3",
            "code": "f59c20"
          }, {
            "minValue": "3",
            "maxValue": "4",
            "code": "#f3bb18"
          },{
            "minValue": "4",
            "maxValue": "5",
            "code": "#f8dd09"
          },{
            "minValue": "5",
            "maxValue": "6",
            "code": "#f7ee12"
          },{
            "minValue": "6",
            "maxValue": "7",
            "code": "#cbd92c"
          },{
            "minValue": "7",
            "maxValue": "8",
            "code": "#abc745"
          },{
            "minValue": "8",
            "maxValue": "9",
            "code": "#7aaea1"
          },{
            "minValue": "9",
            "maxValue": "10",
            "code": "#4496cc"
          },{
            "minValue": "10",
            "maxValue": "11",
            "code": "#317abf"
          },{
            "minValue": "11",
            "maxValue": "12",
            "code": "#3e6db6"
          },{
            "minValue": "12",
            "maxValue": "13",
            "code": "#5e4fa2"
          },{
            "minValue": "13",
            "maxValue": "14",
            "code": "#614096"
          },]
        },
        "value": "10"
      }
    })
    .render();
});
