import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegisterRequest, LoginRequest, User } from '../model/user';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class HttpUserServices {
  private readonly REST_API_SERVER = 'http://localhost:8000/api';

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    }),
  };

  constructor(private httpClient: HttpClient) {}

  // Đăng ký
  register(register: RegisterRequest): Observable<any> {
    const url = `${this.REST_API_SERVER}/auth/register`;
    return this.httpClient.post<any>(url, register, this.httpOptions);
  }

  // Đăng nhập
  login(login: LoginRequest): Observable<any> {
    const url = `${this.REST_API_SERVER}/auth/login`;
    return this.httpClient.post<any>(url, login, this.httpOptions);
  }

  // Lấy thông tin user
  getMe(id: string): Observable<any> {
    const url = `${this.REST_API_SERVER}/auth/${id}`;
    return this.httpClient.get<any>(url, this.httpOptions);
  }
}
