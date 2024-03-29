import { Component, OnInit, NgZone } from '@angular/core';
import { BaseComponent } from '../base/base.component';
import { Incident } from '../../model/incident';
import { IncidentService } from '../../service/incident.service';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import { ChartData } from '../../model/ChartData';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent extends BaseComponent implements OnInit {

  incidents: Incident[];
  cols: any[];
  private chart: am4charts.XYChart;
  input: ChartData[];

  constructor(
    public incidentService: IncidentService,
    private zone: NgZone) { super(); }

  ngOnInit() {
    this.safeSub(
      this.incidentService.getAll().subscribe(
        (incidents) => {
          this.incidents = incidents;
          this.countData();
          this.generateChart();
        }
      )
    );

    this.cols = [
      { field: 'flag', header: 'Flag' },
      { field: 'timestamp', header: 'Timestamp' },
      { field: 'cameraInfo', header: 'CameraInfo' }
    ];
  }

  generateChart() {
    this.zone.runOutsideAngular(() => {
      let chart = am4core.create('chartdiv', am4charts.XYChart)

      chart.legend = new am4charts.Legend()
      chart.legend.position = 'top'
      chart.legend.paddingBottom = 20
      chart.legend.labels.template.maxWidth = 95

      let xAxis = chart.xAxes.push(new am4charts.CategoryAxis())
      xAxis.dataFields.category = 'category'
      xAxis.renderer.cellStartLocation = 0.1
      xAxis.renderer.cellEndLocation = 0.9
      xAxis.renderer.grid.template.location = 0;

      let yAxis = chart.yAxes.push(new am4charts.ValueAxis());
      yAxis.min = 0;

      function createSeries(value, name) {
        let series = chart.series.push(new am4charts.ColumnSeries())
        series.dataFields.valueY = value
        series.dataFields.categoryX = 'category'
        series.name = name
        if (series.name == 'RED') {
          series.columns.template.stroke = am4core.color("#bf231b"); // red outline
          series.columns.template.fill = am4core.color("#bf231b");
        }
        if (series.name == 'YELLOW') {
          series.columns.template.stroke = am4core.color("#ebe700"); // red outline
          series.columns.template.fill = am4core.color("#ebe700");
        }

        let bullet = series.bullets.push(new am4charts.LabelBullet())
        bullet.interactionsEnabled = false
        bullet.dy = 30;
        bullet.label.text = '{valueY}'
        bullet.label.fill = am4core.color('#ffffff')

        return series;
      }

      chart.data = this.input;

      createSeries('red', 'RED');
      createSeries('yellow', 'YELLOW');
    });
  }


  generatePdf() {
    this.incidentService.getPdf()
      .subscribe(res => {
      },
        err => {
          console.log(err);
        })
  }

  countData() {
    this.input = [];
    this.incidents
      .filter((v, i, a) => a.findIndex(t => (t.CameraInfo === v.CameraInfo)) === i)
      .map(({ CameraInfo }) =>
        this.input.push(new ChartData({
          category: CameraInfo,
          red: 0,
          yellow: 0
        })
        )
      );

    this.incidents.forEach(incident => {
      if (incident.Flag === "red") {
        this.input.find(data => data.category === incident.CameraInfo).red += 1;
      }

      if (incident.Flag === "yellow") {
        this.input.find(data => data.category === incident.CameraInfo).yellow += 1;
      }
    })
  }
}
