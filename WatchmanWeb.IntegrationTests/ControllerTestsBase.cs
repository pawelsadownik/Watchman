using System.Net.Http;
using System.Text;
using AutoMapper;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using NUnit.Framework;
using WatchmanWeb.IntegrationTests.Configuration;
using WatchmanWeb.Model;

namespace WatchmanWeb.IntegrationTests
{
    public abstract class ControllerTestsBase
    {
        protected HttpClient _client;
        protected TestWebApplicationFactory _factory;
        protected IMapper _mapper;
        protected ApplicationDbContext _context;

        protected string _uri;

        public ControllerTestsBase(string uri)
        {
            this._uri = uri;
        }
        [OneTimeSetUp]
        public void Setup()
        {
            _factory = new TestWebApplicationFactory();
            _client = _factory.CreateClient(new WebApplicationFactoryClientOptions
            {
                // here some sample options like security tokens etc...
            });
            var services = _factory.Server.Host.Services;
            _context = services.GetRequiredService<ApplicationDbContext>();
            _mapper = services.GetRequiredService<IMapper>();
            var databaseInitializer = services.GetRequiredService<IDatabaseInitializer>();
            databaseInitializer.SeedAsync().Wait();
            JsonConvert.DefaultSettings = () => new JsonSerializerSettings
            {
                ReferenceLoopHandling = ReferenceLoopHandling.Ignore
            };
        }

        [OneTimeTearDown]
        public void TearDown()
        {
            _client.Dispose();
            _factory.Dispose();
        }

        protected StringContent ToJsonStringContent(object obj)
        {
            var content = JsonConvert.SerializeObject(obj);
            return new StringContent(content, Encoding.UTF8, "application/json");
        }

        protected T ToObject<T>(string jsonContent)
        {
            return (T)JsonConvert.DeserializeObject(jsonContent, typeof(T));
        }
    }
}