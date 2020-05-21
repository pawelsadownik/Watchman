import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, catchError, filter, tap } from 'rxjs/operators';
import { UserData } from '../model/userData';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  private url = `api/users`;
  private userData: UserData[] = [];
  private userData$: BehaviorSubject<UserData[]> = new BehaviorSubject<UserData[]>([]);
  private isSaving: boolean;

  constructor(
    private http: HttpClient) { }

  public refresh() {
    return this.http.get<UserData[]>(this.url).subscribe(userData => {
      this.userData = userData;
      this.userData$.next(this.userData);
    });
  }

  public getAll(): Observable<UserData[]> {
    if (this.userData.length === 0) {
      this.refresh();
    }
    return this.userData$;
  }

  public insert(userData: UserData) {
    this.isSaving = true;
    return this.http.post(this.url, userData)
      .pipe(
        map((result: string) => {

          this.isSaving = false;
          return result;
        }),
        catchError(error => {
          console.error(error.message);
          this.isSaving = false;
          return null as string;
        }));
  }

  public update(userData: UserData) {
    this.isSaving = true;
    return this.http.put(this.url, userData)
      .pipe(
        map((result: string) => {
          this.isSaving = false;
          return result;
        }),
        catchError(error => {
          console.error(error.message);
          this.isSaving = false;
          return null as string;
        }));
  }

  public save(userData: UserData) {
    return userData.Id ? this.update(userData) : this.insert(userData);
  }

  public getById(id: string): Observable<UserData> {
    const userData = this.userData.find(userData => userData.Id === id);
    if (!userData && this.userData.length > 0) {
      this.refresh();
    }
    return this.getAll().pipe(
      map(userDataList => userDataList.find(userData => userData.Id === id)),
      filter(userData => userData != null)
    );
  }

  public delete(id: string): Observable<{}> {
    this.isSaving = true;
    return this.http.delete(
      `${this.url}/${id}`)
      .pipe(
        map((result: string) => {
          this.isSaving = false;
          return result;
        }),
        catchError((error) => {
          console.error(error.message);
          this.isSaving = false;
          return null as string;
        }));
  }
}    
