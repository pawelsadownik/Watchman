import { browser, element, by, ElementFinder, protractor } from "protractor";
import { Page } from "./page.po";
import { UserDetailsPage } from "./user-details.po";

export class UsersPage extends Page {

    private usernameColNumber = 0;
    private typeColNumber = 1;
    private actionColNumber =2;

    usersTable = element(by.css("p-table tbody"));
    usersTableRaws = element.all(by.css("p-table tbody tr"));

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
        this.getUserRaw(uname).then( (userTr) => {
            userTr.element(by.css("p-button[label='Edit']")).click();
        });
        return new UserDetailsPage();
    }

    deleteUser(uname:string) :UsersPage {
        this.getUserRaw(uname).then( (userTr) => {
                userTr.element(by.css("td p-button[label='Remove']")).click();
            });
        return new UsersPage;
    }

    getUserRaw(uname:string) {
        let userFound = false;
        let userTr = protractor.promise.defer<ElementFinder>();
        
        this.usersTableRaws.each( function (raw, rawNumber) {
            raw.element(by.css("td:first-child")).getText()
                .then( (v) => {
                    if (v === uname) {
                        userTr.fulfill(raw);
                        userFound = true;
                    }
                }, (reason) => {
                    userTr.reject(reason);
                });
        });

        protractor.promise.controlFlow().execute(function() {
            if (!userFound) {
                userTr.reject(`User ${uname} not found in usersTableRaws`);
            };
        });
        
        return userTr.promise;
    }
}