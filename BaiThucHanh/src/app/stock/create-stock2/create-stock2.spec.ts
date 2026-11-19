import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateStock2 } from './create-stock2';

describe('CreateStock2', () => {
  let component: CreateStock2;
  let fixture: ComponentFixture<CreateStock2>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CreateStock2],
    }).compileComponents();

    fixture = TestBed.createComponent(CreateStock2);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
