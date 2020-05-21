import { Component, OnInit } from '@angular/core';
import { BaseComponent } from '../base/base.component';
import { Incident } from '../../model/incident';
import { IncidentService } from '../../service/incident.service';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css']
})
export class ReportsComponent extends BaseComponent implements OnInit {

  incidents: Incident[] = [];
  cols: any[];

  constructor(
    public incidentService: IncidentService) { super(); }

  ngOnInit() {
    this.safeSub(
      this.incidentService.getAll().subscribe(
        (incidents) => {
          this.incidents = incidents;
        }
      )
    );

    this.cols = [
      { field: 'flag', header: 'Flag' },
      { field: 'timestamp', header: 'Timestamp' },
      { field: 'cameraInfo', header: 'CameraInfo' }
    ];
  }

  generateChart() { }
  generatePdf() { }

}
