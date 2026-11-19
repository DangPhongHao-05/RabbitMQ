// export class Stock {
//   public favorite?: boolean = false;
//   public positiveChange?: boolean;

//   constructor(
//     public name: string,
//     public code: string,
//     public price: number,
//     public previousPrice: number,
//     public exchange: string,
//   ) {
//     this.favorite = false;
//     this.positiveChange = price >= previousPrice;
//   }

//   isPositiveChange(): boolean {
//     return this.price >= this.previousPrice;
//   }
// }

export interface Stock {
  id: string;
  name: string;
  code: string;
  price: number;
  previousPrice: number;
  exchange: string;
  favorite: boolean;
}
