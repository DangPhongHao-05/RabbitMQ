import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { Login } from './login/login';
import { StockItem } from './stock/stock-item/stock-item';
import { CreateStock } from './stock/create-stock/create-stock';
import { FormsModule } from '@angular/forms';
import { CreateStock2 } from './stock/create-stock2/create-stock2';
import { StockList } from './stock/stock-list/stock-list';
import { StockDetail } from './stock/stock-detail/stock-detail';
import { HttpClientModule } from '@angular/common/http';
import { Register } from './register/register';

@NgModule({
  declarations: [
    App,
    Login,
    StockItem,
    CreateStock,
    CreateStock2,
    StockList,
    StockDetail,
    Register,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule, ReactiveFormsModule, HttpClientModule],
  providers: [provideBrowserGlobalErrorListeners()],
  bootstrap: [App],
})
export class AppModule {}
