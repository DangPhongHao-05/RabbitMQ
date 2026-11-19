import { Component } from '@angular/core';
import { Stock } from '../../model/stock';

@Component({
  selector: 'app-create-stock',
  standalone: false,
  templateUrl: './create-stock.html',
  styleUrl: './create-stock.css',
})
export class CreateStock {
  public stock: Stock;
  public confirmed: boolean = false;
  public exchanges = ['NYSE', 'NASDAQ', 'OTHER'];
  constructor() {
    this.stock = {
      id: "1000002928983",
      name: '',
      code: '',
      price: 0,
      previousPrice: 0,
      exchange: 'NYSE',
      favorite: false,
    };
  }

  setStockPrice(price: any) {
    this.stock.price = price;
    this.stock.previousPrice = price;
  }

  createStock(stockForm: any) {
    console.log('Stock form', stockForm);
    if (stockForm.valid) {
      console.log('creating stock', this.stock);
    } else {
      console.error('Stock form is in an invalid state');
    }
  }
}
