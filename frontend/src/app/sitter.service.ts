import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SitterService {

  // baseUrl = "http://127.0.0.1:8000/sitters";
  baseUrl = "http://localhost:8000/sitters/";

  constructor(private http: HttpClient) { }

  getSittersList(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  // getSitter(sitter_id: number): Observable<object width="300" height="150"> {
  getSitter(sitterId: number): Observable<object> {
    return this.http.get(this.baseUrl + sitterId + '/');
  }

  getSittersByRating(rating: number): Observable<any> {
    return this.http.get(this.baseUrl + 'rating/' + rating + '/');
  }
}
