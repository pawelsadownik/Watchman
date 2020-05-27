using System;
using NUnit.Framework;
using System.Net;
using System.Linq;
using WatchmanWeb.ViewModel;

namespace WatchmanWeb.IntegrationTests
{
    [TestFixture]
    public class IncidentControllerTests : ControllerTestsBase

    {
        public IncidentControllerTests() : base("/api/incidents/") { }

        private IncidentVM _requestIncident;

        [SetUp]
        public new void Setup()
        {
            base.Setup();
            _requestIncident = _mapper.Map<IncidentVM>(_context.Incidents.First());
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
            _requestIncident = GetAsNew(_requestIncident);
            var response = _client.PostAsync($"{_uri}", ToJsonStringContent(_requestIncident)).Result;
            Assert.AreEqual(HttpStatusCode.Created, response.StatusCode);
        }

        [Test]
        public void Add_Empty_BadRequestStatus()
        {
            var response = _client.PostAsync($"{_uri}", ToJsonStringContent("")).Result;
            Assert.AreEqual(HttpStatusCode.BadRequest, response.StatusCode);
        }

        private static IncidentVM GetAsNew(IncidentVM vm)
        {
            vm.Id = null;

            return vm;
        }
    }
}
