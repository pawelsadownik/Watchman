import { browser, element, by } from "protractor";
import { Page } from "./page";

export class HomePage extends Page {
    
    get(): HomePage {
        browser.get(this.homeUrl);
        return this;
    }
}