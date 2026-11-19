import { Injectable } from '@angular/core';
import { Stock } from '../model/stock';
import { BehaviorSubject, map, Observable, tap, of } from 'rxjs';
import { HttpStockServices } from './http-stock-services';
import { WebsocketService, StockEvent } from './websocket-service';

@Injectable({
  providedIn: 'root',
})
export class StockServices {
  private stocks: Stock[] = [];
  private stocksSubject = new BehaviorSubject<Stock[]>([]);
  public stocks$: Observable<Stock[]> = this.stocksSubject.asObservable();

  constructor(
    private httpStockServices: HttpStockServices,
    private websocketService: WebsocketService,
  ) {
    this.loadStocks().subscribe();

    this.websocketService.connect();

    this.websocketService.stockEvents$.subscribe((event) => {
      this.handleStockEvent(event);
    });
  }

  private handleStockEvent(event: StockEvent): void {
    const stock = event.data as Stock;

    switch (event.event) {
      case 'stock.created':
        // Thêm cổ phiếu nếu chưa tồn tại
        if (!this.stocks.some((item) => item.id === stock.id)) {
          this.stocks = [...this.stocks, stock];
        }
        break;

      case 'stock.updated':
        // Cập nhật cổ phiếu theo ID
        this.stocks = this.stocks.map((item) => (item.id === stock.id ? stock : item));
        break;

      case 'stock.deleted':
        // Xóa cổ phiếu theo ID
        this.stocks = this.stocks.filter((item) => item.id !== stock.id);
        break;
    }

    // Thông báo cho các component đang theo dõi
    this.stocksSubject.next([...this.stocks]);
  }

  loadStocks(): Observable<Stock[]> {
    return this.httpStockServices.getStock().pipe(
      tap((stocks: Stock[]) => {
        this.stocks = stocks;
        this.stocksSubject.next([...this.stocks]);
      }),
    );
  }

  getStocks(): Observable<Stock[]> {
    return this.stocks$;
  }

  createStock(stock: Stock): Observable<boolean> {
    const foundStock = this.stocks.find((each) => each.code === stock.code);

    if (foundStock) {
      return of(false);
    }

    return this.httpStockServices.postStock(stock).pipe(map(() => true));
  }

  toggleFavorite(stock: Stock): Observable<Stock> {
    const foundStock = this.stocks.find((each) => each.code === stock.code);

    if (!foundStock) {
      throw new Error('Không tìm thấy cổ phiếu');
    }

    const updatedStock = {
      ...foundStock,
      favorite: !foundStock.favorite,
    };

    return this.httpStockServices.updateStock(updatedStock).pipe(
      tap((result: Stock) => {
        this.stocks = this.stocks.map((each) => (each.code === result.code ? result : each));
        this.stocksSubject.next([...this.stocks]);
      }),
    );
  }
  getStockByCode(code: string): Stock | undefined {
    return this.stocks.find((each) => each.code === code);
  }

  updateStock(stock: Stock): Observable<boolean> {
    const foundStock = this.stocks.find((each) => each.code === stock.code);

    if (!foundStock) {
      return new Observable<boolean>((subscriber) => {
        subscriber.next(false);
        subscriber.complete();
      });
    }

    return this.httpStockServices.updateStock(stock).pipe(
      tap((updatedStock: Stock) => {
        this.stocks = this.stocks.map((each) =>
          each.code === updatedStock.code ? updatedStock : each,
        );
        this.stocksSubject.next([...this.stocks]);
      }),
      map(() => true),
    );
  }

  deleteStock(stock: Stock): Observable<boolean> {
    const foundStock = this.stocks.find((each) => each.code === stock.code);

    if (!foundStock) {
      return new Observable<boolean>((subscriber) => {
        subscriber.next(false);
        subscriber.complete();
      });
    }

    return this.httpStockServices.deleteStock(foundStock.id).pipe(
      tap(() => {
        this.stocks = this.stocks.filter((each) => each.code !== foundStock.code);
        this.stocksSubject.next([...this.stocks]);
      }),
      map(() => true),
    );
  }
}
