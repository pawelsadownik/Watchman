import { OnDestroy } from '@angular/core';
import { Subscriber, Subscription } from 'rxjs';

export class BaseComponent implements OnDestroy {
  subscriptionsArray: Subscription[];

  constructor() {
    this.subscriptionsArray = [];
  }
  safeSub(...sub: Subscription[]) {
    this.subscriptionsArray = this.subscriptionsArray.concat(sub);
  }

  ngOnDestroy(): boolean {
    for (let sub of this.subscriptionsArray) {
      if (sub) {
        sub.unsubscribe();
      }
    }
    return true;
  }
}
