var chart = AmCharts.makeChart("chartdiv", {
  "type": "serial",
  "theme": "light",
  "columnWidth": 0.6,
  "dataProvider": [
  {
    "category": "1",
    "count": 64
  }, {
    "category": "2-5",
    "count": 15330
  }, {
    "category": "5-100",
    "count": 6221
  }, {
    "category": "100-200",
    "count": 1196
  },
  {
    "category": "200-1000",
    "count": 926
  },
                   {
    "category": "<1000",
    "count": 123
  }
                  ],
  "graphs": [{
    "fillColors": "#03396c",
    "fillAlphas": 0.9,
    "lineColor": "#fff",
    "lineAlpha": 0.9,
    "type": "column",
    "valueField": "count"
  }],
  "categoryField": "category",
  "categoryAxis": {
    "title": " Node Degree Distribution by %"
  },
  "valueAxes": [{
    "title": "Count",
     "minimum": 0
  }]
});
