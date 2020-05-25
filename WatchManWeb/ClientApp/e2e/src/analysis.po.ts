import { browser, element, by } from "protractor";
import { Page } from "./page";

export class AnalysisPage extends Page {
    
    get(): AnalysisPage {
        browser.get(this.analysisUrl);
        return this;
    }
}