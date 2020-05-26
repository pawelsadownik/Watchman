import { HomePage } from "./home.po";
import { LoginPage } from "./login.po";
import { browser } from "protractor";

describe('Admin navigation', () => {

    let homePage: HomePage;

    beforeEach(() => {
        homePage = new LoginPage().get().doAdminLogin();
    });

    afterEach(() => {
        homePage.clearStorage();
    });

    it('should display admin as current user', () => {
        expect(homePage.getCurrentUser().getText()).toContain('admin');
    });

    it('should be able to go to monitoring', () => {
        homePage.goToMonitoringPage();
        expect(browser.getCurrentUrl()).toContain(homePage.monitoringUrl);
    });

    it('should be able to go to analysis', () => {
        homePage.goToAnalysisPage();
        expect(browser.getCurrentUrl()).toContain(homePage.analysisUrl);
    });

    it('should be able to go to reports', () => {
        homePage.goToReportsPage();
        expect(browser.getCurrentUrl()).toContain(homePage.reportsUrl);
    });
    
    it('should be able to go to users', () => {
        homePage.goToUsersPage();
        expect(browser.getCurrentUrl()).toContain(homePage.usersUrl);
    });

    it('should be able to logout', () => {
        homePage.logOut();
        expect(homePage.getCurrentUser().isPresent()).toBe(false);
    });
    
});

describe('Advanced navigation', () => {

    let homePage: HomePage;

    beforeEach(() => {
        homePage = new LoginPage().get().doAdvancedLogin();
    });

    afterEach(() => {
        homePage.clearStorage();
    });

    it('should display advanced as current user', () => {
        expect(homePage.getCurrentUser().getText()).toContain('advanced');
    });

    it('should be able to go to monitoring', () => {
        homePage.goToMonitoringPage();
        expect(browser.getCurrentUrl()).toContain(homePage.monitoringUrl);
    });

    it('should be able to go to analysis', () => {
        homePage.goToAnalysisPage();
        expect(browser.getCurrentUrl()).toContain(homePage.analysisUrl);
    });

    it('should be able to go to reports', () => {
        homePage.goToReportsPage();
        expect(browser.getCurrentUrl()).toContain(homePage.reportsUrl);
    });
    
    it('should not be able to go to users', () => {
        expect(homePage.navUsers.isPresent()).toBe(false);
    });

    it('should be able to logout', () => {
        homePage.logOut();
        expect(homePage.getCurrentUser().isPresent()).toBe(false);
    });
    
});

describe('Basic navigation', () => {

    let homePage: HomePage;

    beforeEach(() => {
        homePage = new LoginPage().get().doBasicLogin();
    });

    afterEach(() => {
        homePage.clearStorage();
    });

    it('should display basic as current user', () => {
        expect(homePage.getCurrentUser().getText()).toContain('basic');
    });

    it('should be able to go to monitoring', () => {
        homePage.goToMonitoringPage();
        expect(browser.getCurrentUrl()).toContain(homePage.monitoringUrl);
    });

    it('should not be able to go to analysis', () => {
        expect(homePage.navAnalysis.isPresent()).toBe(false);
    });

    it('should not be able to go to reports', () => {
        expect(homePage.navReports.isPresent()).toBe(false);
    });
    
    it('should not be able to go to users', () => {
        expect(homePage.navUsers.isPresent()).toBe(false);
    });

    it('should be able to logout', () => {
        homePage.logOut();
        expect(homePage.getCurrentUser().isPresent()).toBe(false);
    });
    
});
