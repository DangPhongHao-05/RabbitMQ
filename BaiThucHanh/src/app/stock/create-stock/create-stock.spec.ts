import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateStock } from './create-stock';

describe('CreateStock', () => {
  let component: CreateStock;
  let fixture: ComponentFixture<CreateStock>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CreateStock],
    }).compileComponents();

    fixture = TestBed.createComponent(CreateStock);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
