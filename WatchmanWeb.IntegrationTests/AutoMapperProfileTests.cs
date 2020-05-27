using System;
using AutoMapper;
using NUnit.Framework;
using WatchmanWeb.Mappings;

namespace WatchmanWeb.IntegrationTests
{
    public class AutoMapperProfileTests
    {
        [Test]
        public void AutoMapper_Configuration_IsValid()
        {
            try
            {
                var config = new MapperConfiguration(cfg =>
                {
                    cfg.AddProfile(new AutoMapperWebProfile());
                });
                config.CreateMapper();
                config.AssertConfigurationIsValid();
                Assert.Pass();
            }
            catch (AutoMapperConfigurationException ex)
            {
                Console.WriteLine(ex.Message);
                Assert.Fail();
            }
        }
    }
}