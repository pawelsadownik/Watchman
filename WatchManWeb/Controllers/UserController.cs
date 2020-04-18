using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using WatchmanWeb.Model;

namespace WatchmanWeb.Controllers
{
    [Route("api/[controller]")]
    public class UserController : Controller
    {
        [HttpGet]
        [Route("GetAdminData")]
        [Authorize(Policy = Policies.Admin)]
        public IActionResult GetAdminData()
        {
            return Ok("This is an admin user");
        }

        [HttpGet]
        [Route("GetAdvancedUserData")]
        [Authorize(Policy = Policies.AdvancedUser)]
        public IActionResult GetAdvancedUserData()
        {
            return Ok("This is an advanced user");
        }

        [HttpGet]
        [Route("GetBasicUserData")]
        [Authorize(Policy = Policies.BasicUser)]
        public IActionResult GetBasicUserData()
        {
            return Ok("This is a basic user");
        }
    }
}
