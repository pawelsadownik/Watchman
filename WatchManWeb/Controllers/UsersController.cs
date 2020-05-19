using AutoMapper;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using WatchmanWeb.Model;
using WatchmanWeb.Services;
using WatchmanWeb.ViewModel;

namespace WatchmanWeb.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {
        private readonly IUserService _userService;
        private readonly IMapper _mapper;
        public UsersController(IUserService userService, IMapper mapper)
        {
            _userService = userService;
            _mapper = mapper;
        }

        [HttpGet]
        public List<UserVM> GetAll()
        {
            return _mapper.Map<List<UserVM>>(_userService.GetAll());
        }

        [HttpGet("{id}")]
        public UserVM GetById(Guid id)
        {
            var user = _userService.GetById(id);
            return _mapper.Map<UserVM>(user);
        }

        [HttpPost]
        public async Task<IActionResult> Add([FromBody] UserVM userVM)
        {
            var user = _mapper.Map<User>(userVM);

            _userService.Add(user);
            return Created("/api/user", _mapper.Map<UserVM>(user).Id);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            _userService.Remove(id);
            return Ok();
        }

        [HttpPut]
        public async Task<IActionResult> Update([FromBody] UserVM userVM)
        {
            if (userVM == null)
            {
                return BadRequest();
            }
            _userService.Update(_mapper.Map<User>(userVM));
            return Ok();
        }       
    }
}
