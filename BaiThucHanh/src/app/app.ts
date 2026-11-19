import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from './services/user-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: false,
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('BaiThucHanh');
  constructor(
    public router: Router,
    public userService: UserService,
  ) {}

  logout(): void {
    this.userService.logout();
    this.router.navigate(['/login']);
  }
}
