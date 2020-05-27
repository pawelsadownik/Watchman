import { browser, element, by } from "protractor";
import { Page } from "./page.po";

export class ReportsPage extends Page {
    
    get(): ReportsPage {
        browser.get(this.reportsUrl);
        return this;
    }
}