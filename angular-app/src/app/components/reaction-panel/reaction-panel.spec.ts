import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReactionPanel } from './reaction-panel';

describe('ReactionPanel', () => {
  let component: ReactionPanel;
  let fixture: ComponentFixture<ReactionPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReactionPanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReactionPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
