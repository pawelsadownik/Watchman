import { browser, element, by, ElementFinder } from "protractor";
import { Page } from "./page.po";
import { UserDetailsPage } from "./user-details.po";

export class UsersPage extends Page {

    private usernameColNumber = 1;
    private typeColNumber = 2;
    private actionColNumber =3;

    private usersTable = element(by.css("p-table table"));
    private usersTableRaws = element.all(by.css("p-table table tr"));

    readonly btnCreateUser = element(by.id("create-user"));
    
    get(): UsersPage {
        browser.get(this.usersUrl);
        return this;
    }
    
    getUser(uname:string) :ElementFinder {
        return this.usersTable.element(by.cssContainingText('tr td:first-child', uname));
    }

    goToCreateUser() :UserDetailsPage {
        this.btnCreateUser.click();
        return new UserDetailsPage();
    }

    goToEditUser(uname:string) :UserDetailsPage {
        this.getUserRaw(uname).all(by.tagName("td")).get(this.actionColNumber).element(by.css("p-button[label='Edit'")).click();
        return new UserDetailsPage();
    }
//TODO delete confirmation
    deleteUser(uname:string) {
        this.getUserRaw(uname).all(by.tagName("td")).get(this.actionColNumber).element(by.css("p-button[label='Remove'")).click();;
    }

    getUserRaw(uname:string) :ElementFinder {
        let userRaw = -1;
        this.usersTableRaws.each( function (raw, rawNumber) {
            if(raw.element(by.cssContainingText('tr td:first-child', uname)).isPresent())
                userRaw=rawNumber;
        });
        if (userRaw=-1) return;
        return this.usersTableRaws.get(userRaw);
    }
}