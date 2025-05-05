# F5 GSLB (Global Server Load Balancing)

F5 GSLB, also known as **F5 DNS** (formerly GTM – Global Traffic Manager), is a solution used to distribute traffic across multiple geographically dispersed data centers or cloud regions.

---

##  Core Functionality of F5 GSLB

### DNS-Based Load Balancing
- Operates primarily at the **DNS level**.
- When a client requests a domain (e.g., `app.example.com`), the DNS query is routed to the **F5 BIG-IP DNS module**.
- F5 decides which data center or server to direct the user to and returns the corresponding IP address.

### Intelligent Traffic Steering
F5 chooses the best destination based on:
- **Proximity/Latency** – Direct users to the nearest or lowest-latency data center.
- **Health Checks** – Ensure the selected destination is up and available.
- **Load** – Balance traffic based on utilization across sites.
- **Geolocation** – Route users based on geographic policies.
- **Persistence** – Maintain session stickiness when required.

### Health Monitoring
- Active health checks (HTTP, HTTPS, TCP, etc.) ensure only healthy endpoints are returned.
- If a service or site is down, F5 GSLB automatically reroutes to another healthy location.

### Wide IPs and Pools
- **Wide IP**: The DNS name users query (e.g., `login.example.com`).
- **Pools**: Groups of virtual servers/IPs that the Wide IP can resolve to.
- Each pool member can have assigned priority and a load balancing method.

### Integration with LTM
- F5 GSLB often works alongside **F5 LTM (Local Traffic Manager)**.
- **LTM** handles local traffic; **GSLB** handles traffic between sites.

### Topology Records (Optional)
- Admins can define routing rules (e.g., users in Europe go to the EU data center).

---

##  Example Workflow

1. User types `app.example.com` into a browser.
2. DNS query is intercepted by **F5 GSLB**.
3. F5 evaluates:
   - Are sites healthy?
   - Which site is closest?
   - Are any load thresholds exceeded?
4. F5 returns the IP of the optimal virtual server.
5. User's browser connects to that IP.

---

##  GSLB with Multiple Pools (Primary & Secondary)

This setup prefers **Primary Pool** members (main data center) and falls back to **Secondary Pool** members (backup/DR site) if necessary.

---

## ⚙️ Step-by-Step Operation

### Wide IP
- DNS entry queried by users (e.g., `app.example.com`)

### Pools Configuration
- **Primary Pool**: Servers in the preferred/main data center.
- **Secondary Pool**: Servers in the backup/DR site.

### Pool Members
- Each pool has virtual servers (VIPs) with health checks.

### Load Balancing Method
- Example: **Global Availability**
  - Pools are evaluated in priority order.
  - F5 uses the **Primary Pool** if any member is healthy.
  - Fails over to **Secondary Pool** if the primary is down.

---

## Example Configuration Summary

**Wide IP**: `app.example.com`

### Pool 1 (Primary)
- Site A – `10.0.0.1`
- Site A – `10.0.0.2`

### Pool 2 (Secondary)
- Site B – `20.0.0.1`
- Site B – `20.0.0.2`

- **Health Monitors**: Enabled on all members
- **Load Balancing**: Global Availability

---

## Logic Diagram 
<img src="f5-gslb.png" width="800">
