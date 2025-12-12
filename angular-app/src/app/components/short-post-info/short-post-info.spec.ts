import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShortPostInfo } from './short-post-info';

describe('ShortPostInfo', () => {
  let component: ShortPostInfo;
  let fixture: ComponentFixture<ShortPostInfo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShortPostInfo]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShortPostInfo);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
