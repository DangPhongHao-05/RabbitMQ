import { Injectable } from '@angular/core';
import { HttpUserServices } from './http-user-services';
import { Observable, tap, switchMap, map } from 'rxjs';
import { LoginRequest, RegisterRequest, User } from '../model/user';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private user?: User;

  constructor(private httpUserServices: HttpUserServices) {}

  // Lấy thông tin người dùng hiện tại
  loadUser(): Observable<User> {
    if (!this.user?.id) {
      throw new Error('Chưa có người dùng đăng nhập');
    }

    return this.httpUserServices.getMe(this.user.id).pipe(
      map((res) => res.user as User),
      tap((user) => {
        this.user = user;
      }),
    );
  }

  // Đăng ký
  register(data: RegisterRequest): Observable<any> {
    return this.httpUserServices.register(data);
  }

  // Đăng nhập và lấy thông tin người dùng
  login(data: LoginRequest): Observable<User> {
    return this.httpUserServices.login(data).pipe(
      map((res) => res.user.id as string),
      switchMap((id) => this.httpUserServices.getMe(id)),
      map((res) => res.user as User),
      tap((user) => {
        this.user = user;
      }),
    );
  }

  // Lấy người dùng hiện tại
  getUser(): User | undefined {
    return this.user;
  }

  // Kiểm tra đăng nhập
  isLoggedIn(): boolean {
    return !!this.user;
  }

  // Đăng xuất
  logout(): void {
    this.user = undefined;
  }
}
