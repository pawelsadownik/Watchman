import { Injectable } from '@angular/core';
import { Incident } from '../model/incident';
import { Observable, BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class IncidentService {

  private url = `api/incidents`;
  private incidents: Incident[] = [];
  private incidents$: BehaviorSubject<Incident[]> = new BehaviorSubject<Incident[]>([]);

  constructor(
    private http: HttpClient) { }

  public refresh() {
    return this.http.get<Incident[]>(this.url).subscribe(incidents => {
      this.incidents = incidents;
      this.incidents$.next(this.incidents);
    });
  }

  public getAll(): Observable<Incident[]> {
    if (this.incidents.length === 0) {
      this.refresh();
    }
    return this.incidents$;
  }
}    
