import { browser, element, by } from "protractor";
import { Page } from "./page";

export class MonitoringPage extends Page {
    
    get(): MonitoringPage {
        browser.get(this.monitoringUrl);
        return this;
    }
}