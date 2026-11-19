import { Component, OnInit, TemplateRef, ViewChild, ChangeDetectorRef } from '@angular/core';
import { Stock } from '../../model/stock';
import { MatDialog } from '@angular/material/dialog';
import { StockServices } from '../../services/stockservices';
import { CreateStock2 } from '../create-stock2/create-stock2';
import { StockDetail } from '../stock-detail/stock-detail';
import { catchError, EMPTY, Subject, switchMap, take, takeUntil, timer } from 'rxjs';

@Component({
  selector: 'app-stock-list',
  standalone: false,
  templateUrl: './stock-list.html',
  styleUrl: './stock-list.css',
})
export class StockList implements OnInit {
  private destroy$ = new Subject<void>();
  @ViewChild('dialogTemplate') dialogTemplate!: TemplateRef<any>;
  public stocks: Stock[] = [];

  constructor(
    private dialog: MatDialog,
    private stockServices: StockServices,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.stockServices
      .getStocks()
      .pipe(takeUntil(this.destroy$))
      .subscribe((stocks) => {
        console.log('Danh sách cổ phiếu thay đổi:', stocks);

        this.stocks = stocks;
        this.cdr.detectChanges();
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  // ngOnInit() {
  //   this.stocks = this.stockServices.getStocks();
  //   this.cdr.detectChanges();
  // }
  onToggleFavorite(stock: Stock) {
    this.stockServices.toggleFavorite(stock).subscribe({
      next: () => {
        console.log('Cập nhật yêu thích thành công');
      },
      error: (err) => {
        console.error('Lỗi cập nhật yêu thích:', err);
      },
    });
  }

  openCreateStock() {
    this.dialog.open(this.dialogTemplate, {
      width: '600px',
      autoFocus: false,
    });
  }

  deleteStock(stock: Stock) {
    this.stockServices.deleteStock(stock).subscribe({
      next: (success) => {
        if (success) {
          console.log('Xóa cổ phiếu thành công');
        } else {
          console.log('Không tìm thấy cổ phiếu');
        }
      },
      error: (err) => {
        console.error('Lỗi xóa cổ phiếu:', err);
      },
    });
  }

  updateStock(stock: Stock) {
    this.dialog.open(CreateStock2, {
      width: '600px',
      autoFocus: false,
      data: stock,
    });
  }

  viewStock(stock: Stock) {
    const foundStock = this.stockServices.getStockByCode(stock.code);

    if (foundStock) {
      this.dialog.open(StockDetail, {
        width: '500px',
        data: foundStock,
      });
    }
  }
}
