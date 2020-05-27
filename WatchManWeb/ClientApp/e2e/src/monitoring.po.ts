import { browser, element, by } from "protractor";
import { Page } from "./page.po";

export class MonitoringPage extends Page {
    
    get(): MonitoringPage {
        browser.get(this.monitoringUrl);
        return this;
    }
}