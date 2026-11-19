import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Stock } from '../model/stock';
import { UserService } from './user-service';

@Injectable({
  providedIn: 'root',
})
export class HttpStockServices {
  private readonly REST_API_SERVER = 'http://localhost:8000/api';

  constructor(
    private httpClient: HttpClient,
    private userService: UserService,
  ) {}

  // Lấy header chứa ID người dùng
  private getHeaders(): HttpHeaders {
    const user = this.userService.getUser();
    console.log('User hiện tại:', user);
    console.log('User ID gửi lên:', user?.id);
    if (!user?.id) {
      throw new Error('Bạn chưa đăng nhập!');
    }

    return new HttpHeaders({
      'Content-Type': 'application/json',
      'X-User-Id': user.id,
    });
  }

  // GET: Lấy danh sách cổ phiếu
  getStock(): Observable<any> {
    const url = `${this.REST_API_SERVER}/stocks/`;

    return this.httpClient.get<any>(url);
  }

  // POST: Thêm cổ phiếu
  postStock(data: Stock): Observable<any> {
    const url = `${this.REST_API_SERVER}/stocks/`;

    return this.httpClient.post<any>(url, data, {
      headers: this.getHeaders(),
    });
  }

  // PUT: Cập nhật cổ phiếu
  updateStock(stock: Stock): Observable<any> {
    const url = `${this.REST_API_SERVER}/stocks/${encodeURIComponent(stock.id)}`;

    return this.httpClient.put<any>(url, stock, {
      headers: this.getHeaders(),
    });
  }

  // DELETE: Xóa cổ phiếu
  deleteStock(id: string): Observable<any> {
    const url = `${this.REST_API_SERVER}/stocks/${encodeURIComponent(id)}`;

    return this.httpClient.delete<any>(url, {
      headers: this.getHeaders(),
    });
  }
}
