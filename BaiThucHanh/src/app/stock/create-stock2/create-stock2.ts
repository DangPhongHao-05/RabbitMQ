import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Stock } from '../../model/stock';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { StockServices } from '../../services/stockservices';

let counter = 1;

@Component({
  selector: 'app-create-stock2',
  standalone: false,
  templateUrl: './create-stock2.html',
  styleUrl: './create-stock2.css',
})
export class CreateStock2 {
  public stockForm!: FormGroup;
  public stock!: Stock;
  public exchanges = ['NSE', 'NYSE', 'NASDAQ'];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CreateStock2>,
    private stockServices: StockServices,
    @Inject(MAT_DIALOG_DATA) public data: Stock,
  ) {
    this.createForm();
    this.stock = {
      id: "18263",
      name: 'Test' + counter++,
      code: 'T&T',
      price: 20,
      previousPrice: 10,
      exchange: 'NSE',
      favorite: false,
    };
    if (this.data) {
      this.stockForm.patchValue({
        name: this.data.name,
        code: this.data.code,
        price: this.data.price,
        exchange: this.data.exchange,
        agree: true,
      });
    }
  }

  createForm() {
    this.stockForm = this.fb.group({
      name: [null, [Validators.required]],
      code: [null, [Validators.required, Validators.minLength(2)]],
      price: [0, [Validators.required, Validators.min(0)]],
      exchange: ['', [Validators.required]],
      agree: [false, [Validators.requiredTrue]],
    });
  }

  onSubmit() {
    if (this.stockForm.valid) {
      const val = this.stockForm.value;
      const stock: Stock = {
        id: this.data ? this.data.id : "0",
        name: val.name,
        code: val.code,
        price: Number(val.price),
        previousPrice: this.data ? this.data.previousPrice : Number(val.price),
        exchange: val.exchange,
        favorite: this.data ? this.data.favorite : false,
      };

      if (this.data) {
        this.stockServices.updateStock(stock).subscribe({
          next: (success) => {
            if (success) {
              this.dialogRef.close();
            } else {
              alert('Stock code not found');
            }
          },
          error(err) {
            console.error('Error update stock', err);
          },
        });
      } else {
        this.stockServices.createStock(stock).subscribe({
          next: (success) => {
            if (success) {
              (this.stockForm.reset(), this.dialogRef.close());
            } else {
              alert('Stock code is exists');
            }
          },
          error(err) {
            console.error('Error create stock', err);
          },
        });
      }
    } else {
      this.stockForm.markAllAsTouched();
    }
  }

  loadStockFromServer() {
    this.stock = {
      id: "93893484",
      name: `Test ${counter++}`,
      code: 'T&T',
      price: 20,
      previousPrice: 10,
      exchange: 'NSE',
      favorite: false,
    };
    let stockFormModel = Object.assign({}, this.stock);
    // delete stockFormModel.positiveChange;
    // delete stockFormModel.favorite;
    this.stockForm.setValue({
      ...stockFormModel,
      agree: true,
    });
  }

  patchStockForm() {
    this.stock = {
      id: "187276364",
      name: `Test ${counter++}`,
      code: 'T&T',
      price: 20,
      previousPrice: 10,
      exchange: 'NSE',
      favorite: false,
    };
    this.stockForm.patchValue(this.stock);
  }

  resetForm() {
    this.stockForm.reset();
  }

  get name() {
    return this.stockForm.get('name');
  }

  get price() {
    return this.stockForm.get('price');
  }

  get code() {
    return this.stockForm.get('code');
  }

  get exchange() {
    return this.stockForm.get('exchange');
  }

  get agree() {
    return this.stockForm.get('agree');
  }

  closeDialog() {
    this.dialogRef.close('dialog đã đóng');
  }
}
