import { browser, element, by } from "protractor";
import { Page } from "./page.po";

export class HomePage extends Page {
    
    get(): HomePage {
        browser.get(this.homeUrl);
        return this;
    }
}