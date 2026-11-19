import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface StockEvent {
  event: 'stock.created' | 'stock.updated' | 'stock.deleted';
  data: any;
}

@Injectable({
  providedIn: 'root',
})
export class WebsocketService {
  private socket?: WebSocket;

  private stockEventSubject = new Subject<StockEvent>();

  stockEvents$ = this.stockEventSubject.asObservable();

  connect(): void {
    // Không tạo kết nối trùng lặp
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.socket = new WebSocket('ws://127.0.0.1:8000/ws/stocks');

    this.socket.onopen = () => {
      console.log('Đã kết nối WebSocket!');
    };

    this.socket.onmessage = (message) => {
      const event: StockEvent = JSON.parse(message.data);

      console.log('Nhận sự kiện cổ phiếu:', event);

      this.stockEventSubject.next(event);
    };

    this.socket.onerror = (error) => {
      console.error('Lỗi WebSocket:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket đã ngắt kết nối!');
    };
  }

  disconnect(): void {
    this.socket?.close();
    this.socket = undefined;
  }
}
