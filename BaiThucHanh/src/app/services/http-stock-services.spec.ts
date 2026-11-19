import { TestBed } from '@angular/core/testing';

import { HttpStockServices } from './http-stock-services';

describe('HttpStockServices', () => {
  let service: HttpStockServices;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HttpStockServices);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
