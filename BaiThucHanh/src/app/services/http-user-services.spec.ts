import { TestBed } from '@angular/core/testing';

import { HttpUserServices } from './http-user-services';

describe('HttpUserServices', () => {
  let service: HttpUserServices;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HttpUserServices);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
