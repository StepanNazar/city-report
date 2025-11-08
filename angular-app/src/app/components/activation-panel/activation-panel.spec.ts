import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivationPanel } from './activation-panel';

describe('ActivationPanel', () => {
  let component: ActivationPanel;
  let fixture: ComponentFixture<ActivationPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActivationPanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ActivationPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
