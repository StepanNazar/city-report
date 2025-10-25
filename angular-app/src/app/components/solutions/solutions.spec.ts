import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Solutions } from './solutions';

describe('Solutions', () => {
  let component: Solutions;
  let fixture: ComponentFixture<Solutions>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Solutions]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Solutions);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
