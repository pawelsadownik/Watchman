import { browser, element, by } from "protractor";
import { Page } from "./page";

export class UsersPage extends Page {
    
    get(): UsersPage {
        browser.get(this.usersUrl);
        return this;
    }
}