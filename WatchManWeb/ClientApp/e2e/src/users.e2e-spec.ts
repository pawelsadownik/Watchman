import { UsersPage } from "./users.po";
import { LoginPage } from "./login.po";

describe('Users Page', () => {

    let usersPage: UsersPage;

    beforeEach(() => {
        usersPage = new LoginPage().get().doAdminLogin().goToUsersPage();
    });

    afterEach(() => {
        usersPage.clearStorage();
    });

    it('should create user button be visible', () => {
        expect(usersPage.btnCreateUser.isPresent()).toBe(true);
    });

    xit('should create test user', () => {
        expect(usersPage.goToCreateUser().createTestUser().getUser(this.testFirstName).isPresent()).toBe(true);
    });

});