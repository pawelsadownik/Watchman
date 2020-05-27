using System;
using NUnit.Framework;
using System.Net;
using System.Linq;
using WatchmanWeb.ViewModel;

namespace WatchmanWeb.IntegrationTests
{
    [TestFixture]
    public class UserControllerTests : ControllerTestsBase

    {
        public UserControllerTests() : base("/api/users/") {}

        private UserVM _requestUser;

        [SetUp]
        public new void Setup()
        {
            base.Setup();
            _requestUser = _mapper.Map<UserVM>(_context.Users.First());
        }

        [Test]
        public void GetAll_WithoutParameters_ReturnOKStatus()
        {
            var response = _client.GetAsync(_uri).Result;
            Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
        }

        [Test]
        public void Add_CorrectlyFilledViewModel_CreatedStatus()
        {
            _requestUser = GetAsNew(_requestUser);
            var response = _client.PostAsync($"{_uri}", ToJsonStringContent(_requestUser)).Result;
            Assert.AreEqual(HttpStatusCode.Created, response.StatusCode);
        }

        [Test]
        public void Add_Empty_BadRequestStatus()
        {
            var response = _client.PostAsync($"{_uri}", ToJsonStringContent("")).Result;
            Assert.AreEqual(HttpStatusCode.BadRequest, response.StatusCode);
        }

        [Test]
        public void Delete_CorrectUserId_OkStatus()
        {
            var delete = _client.DeleteAsync($"{_uri}{_requestUser.Id}").Result;
            Assert.AreEqual(HttpStatusCode.OK, delete.StatusCode);
        }

        [Test]
        public void Delete_InCorrectUserId_BadRequestStatus()
        {
            var delete = _client.DeleteAsync($"{_uri}{Guid.NewGuid()}").Result;
            Assert.AreEqual(HttpStatusCode.BadRequest, delete.StatusCode);
        }

        [Test]
        public void Update_User_OkStatus()
        {
            var update = _client.PutAsync(_uri, ToJsonStringContent(_requestUser)).Result;
            Assert.AreEqual(HttpStatusCode.OK, update.StatusCode);
        }

        private static UserVM GetAsNew(UserVM vm)
        {
            vm.Id = null;

            return vm;
        }
    }

}

