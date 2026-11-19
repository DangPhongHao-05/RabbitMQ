import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Stock } from '../../model/stock';

@Component({
  selector: 'app-stock-item',
  standalone: false,
  templateUrl: './stock-item.html',
  styleUrl: './stock-item.css',
})
export class StockItem implements OnInit {
  constructor() {}
  @Input() stock!: Stock & { styles?: any };
  @Output() delete = new EventEmitter<Stock>();
  @Output() update = new EventEmitter<Stock>();
  @Output() detail = new EventEmitter<Stock>();
  @Output() favorite = new EventEmitter<Stock>();

  ngOnInit(): void {
    // if (this.stock) {
    //   let diff = this.stock.price / this.stock.previousPrice - 1;
    //   let largeChange = Math.abs(diff) > 0.01;

    //   this.stock.styles = {
    //     color: this.stock.isPositiveChange() ? 'green' : 'red',
    //     'font-size': largeChange ? '1.2em' : '0.8em',
    //   };
    // }
  }

  deleteStock() {
    this.delete.emit(this.stock);
  }

  updateStock() {
    this.update.emit(this.stock);
  }

  viewStock() {
    this.detail.emit(this.stock);
  }

  onToggleFavorite() {
    this.favorite.emit(this.stock);
  }
}
