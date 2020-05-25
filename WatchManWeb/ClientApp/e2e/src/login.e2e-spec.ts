import { browser } from "protractor";
import { LoginPage } from "./login.po";

describe('Login Page', () => {
    let loginPage: LoginPage;

    beforeEach(() => {
        loginPage = new LoginPage();
    });

    it('should be login page actually', () => {
        loginPage.get();
        expect(loginPage.getLoginForm().isPresent()).toBe(true);
    });

    it('should login as admin', () => {
        loginPage.get();
        loginPage.doAdminLogin();
        expect(browser.getTitle()).toEqual('WATCHMAN');
        loginPage.logOut();
    });

});