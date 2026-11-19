import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Stock } from '../../model/stock';

@Component({
  selector: 'app-stock-detail',
  standalone: false,
  templateUrl: './stock-detail.html',
  styleUrl: './stock-detail.css',
})
export class StockDetail {
  constructor(
    private dialogRef: MatDialogRef<StockDetail>,
    @Inject(MAT_DIALOG_DATA) public stock: Stock,
  ) {}

  closeDialog() {
    this.dialogRef.close();
  }
}
