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

    it('should create test user and delete after', () => {
        expect(usersPage
            .goToCreateUser()
            .createTestUser()
            .btnCreateUser
            .isPresent()
        ).toBe(true);
        expect(usersPage.getUser(usersPage.testUsername).isPresent()).toBe(true);
        usersPage.deleteUser(usersPage.testUsername);
        expect(usersPage.getUser(usersPage.testUsername).isPresent()).toBe(false);
    });
});