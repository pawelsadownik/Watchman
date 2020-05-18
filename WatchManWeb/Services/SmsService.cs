using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WatchmanWeb.Services
{
    public interface ISmsService
    {
        void SendSms(string phoneNumber);
    }
    public class SmsService : ISmsService
    {
        private readonly IConfiguration _config;

        public SmsService(IConfiguration config)
        {
            _config = config;
        }

        public void SendSms(string phoneNumber)
        {
            try
            {
                SMSApi.Api.IClient client = new SMSApi.Api.ClientOAuth(_config["Smsapi:Token"]);

                var smsApi = new SMSApi.Api.SMSFactory(client);

                var result =
                    smsApi.ActionSend()
                        .SetText("WATCHMAN ALERT: Terminal 2,  TIME: " + DateTime.Now + " Hurry Up!!!")
                        .SetTo(phoneNumber)
                        .SetSender("Test")
                        .Execute();

                Console.WriteLine("Send: " + result.Count);

                string[] ids = new string[result.Count];

                for (int i = 0, l = 0; i < result.List.Count; i++)
                {
                    if (!result.List[i].isError())
                    {
                        if (!result.List[i].isFinal())
                        {
                            ids[l] = result.List[i].ID;
                            l++;
                        }
                    }
                }

                Console.WriteLine("Get:");
                result =
                    smsApi.ActionGet()
                        .Ids(ids)
                        .Execute();

                foreach (var status in result.List)
                {
                    Console.WriteLine("ID: " + status.ID + " NUmber: " + status.Number + " Points:" + status.Points + " Status:" + status.Status + " IDx: " + status.IDx);
                }

                for (int i = 0, l = 0; i < result.List.Count; i++)
                {
                    if (!result.List[i].isError())
                    {
                        var deleted =
                            smsApi.ActionDelete()
                                .Id(result.List[i].ID)
                                .Execute();
                        Console.WriteLine("Deleted: " + deleted.Count);
                    }
                }
            }
            catch (SMSApi.Api.ActionException e)
            {
                System.Console.WriteLine(e.Message);
            }
            catch (SMSApi.Api.ClientException e)
            {
                /**
				 * Error codes (list available in smsapi docs). Example:
				 * 101 	Invalid authorization info
				 * 102 	Invalid username or password
				 * 103 	Insufficient credits on Your account
				 * 104 	No such template
				 * 105 	Wrong IP address (for IP filter turned on)
				 * 110	Action not allowed for your account
				 */
                Console.WriteLine(e.Message);
            }
            catch (SMSApi.Api.HostException e)
            {
                /* 
				 * Server errors
				 * SMSApi.Api.HostException.E_JSON_DECODE - problem with parsing data
				 */
                Console.WriteLine(e.Message);
            }
            catch (SMSApi.Api.ProxyException e)
            {
                // communication problem between client and sever
                Console.WriteLine(e.Message);
            }
        }
    }
}
