import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateStock } from './stock/create-stock/create-stock';
import { CreateStock2 } from './stock/create-stock2/create-stock2';
import { StockList } from './stock/stock-list/stock-list';
import { Login } from './login/login';
import { Register } from './register/register';

const routes: Routes = [
  { path: '', component: Login },
  { path: 'create-stock', component: CreateStock },
  { path: 'create-stock2', component: CreateStock2 },
  {path: 'stock-list', component: StockList},
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: '**', redirectTo: 'register' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
