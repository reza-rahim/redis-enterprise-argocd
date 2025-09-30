```

- name: Wait until all pods have all containers READY (n/n)
  ansible.builtin.shell: |
    set -o pipefail
    oc get pods -A --no-headers | awk '{
      split($2,a,"/");              # a[1] = ready, a[2] = total
      # flag as not-ready if: there are containers AND not all ready AND not a completed job
      if (a[2] > 0 && a[1] != a[2] && $4 != "Completed" && $4 != "Succeeded") {
        printf "%-20s %-55s %-8s %-12s\n", $1, $2, $3, $4; 
        bad=1
      }
    } END { exit bad }'
  args:
    executable: /bin/bash
  register: pods_check
  changed_when: false
  retries: 60        # try up to 10 minutes total
  delay: 10
  until: pods_check.rc == 0


```

```
- name: Wait until cluster test results are all true
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Poll cluster status
      uri:
        url: "http://your-api-endpoint/cluster/status"
        method: GET
        return_content: yes
      register: cluster_status
      until: >
        (cluster_status.json.cluster_test_result | bool) and
        (cluster_status.json.nodes | map(attribute='result') | list | unique == [true])
      retries: 30
      delay: 10
      failed_when: cluster_status.json is not defined



```

```
ids:
{% for id in rerc_list %}
  - {{ id }}
{% endfor %}

```

```
- set_fact:
    rerc_list: >-
      {{
        ocp_targets
        | map(attribute='name')
        | zip(ocp_targets | map(attribute='namespace'))
        | map('join','-')
        | map('regex_replace','^','rerc-')
        | list
      }}

```
```
- hosts: localhost
  gather_facts: no
  vars:
    ocp_targets:
      - { ocp_cluster: "a", namespace: "n1" }
      - { ocp_cluster: "b", namespace: "n2" }
      - { ocp_cluster: "c", namespace: "n3" }

  roles:
    - role: main_role
      vars:
        ocp_cluster: "{{ item.ocp_cluster }}"
        namespace: "{{ item.namespace }}"
      loop: "{{ ocp_targets }}"
      loop_control:
        label: "{{ item.ocp_cluster }}:{{ item.namespace }}"

    - role: final_role
      vars:
        all_targets: "{{ ocp_targets }}"
        last_target: "{{ ocp_targets[-1] }}"
        is_final: true
```
```
---
- name: Run roles with last-element handling
  hosts: localhost
  gather_facts: no
  vars:
    ocp_targets:
      - { ocp_cluster: "a", namespace: "n1" }
      - { ocp_cluster: "b", namespace: "n2" }
      - { ocp_cluster: "c", namespace: "n3" }

  tasks:
    - name: Run main role for each cluster/namespace
      include_role:
        name: main_role
      vars:
        ocp_cluster: "{{ item.ocp_cluster }}"
        namespace: "{{ item.namespace }}"
      loop: "{{ ocp_targets }}"

    - name: Run special role only for last element
      include_role:
        name: final_role
      vars:
        ocp_cluster: "{{ item.ocp_cluster }}"
        namespace: "{{ item.namespace }}"
      loop: "{{ ocp_targets }}"
      when: loop.last


```


```
- name: Run if 'admin' does NOT exist
  ansible.builtin.debug:
    msg: "Admin is missing, need to create"
  when: users_list | selectattr('name', 'equalto', 'admin') | list | length == 0
```
```
ldap:
    # REQUIRED: which LDAP protocol to use
    # Allowed: LDAP | LDAPS | STARTTLS
    protocol: LDAPS

    # One or more LDAP servers
    servers:
      - host: ldap1.example.com
        port: 636        # defaults: 389 for LDAP/STARTTLS, 636 for LDAPS
      - host: ldap2.example.com
        port: 636

    # Bind credentials (Secret in same namespace, keys: dn, password)
    bindCredentialsSecretName: ldap-bind-cred

    # CA cert for LDAPS / STARTTLS (Secret key: cert)
    caCertificateSecretName: ldap-ca-cert

    # (Optional) timeouts & caching
    directoryTimeoutSeconds: 5
    cacheTTLSeconds: 60

    # Turn on LDAP for control-plane (REC UI/API) and/or data-plane (DB users)
    enabledForControlPlane: true
    enabledForDataPlane: true

    # REQUIRED: how to find the user's DN to authenticate (pick ONE style)

    # Option A: template (simple and common)
    authenticationQuery:
      template: "uid=%u,ou=people,dc=example,dc=com"

    # Option B: search query (mutually exclusive with template)
    # authenticationQuery:
    #   query:
    #     base: "ou=people,dc=example,dc=com"
    #     filter: "(uid=%u)"
    #     scope: WholeSubtree   # BaseObject | SingleLevel | WholeSubtree

    # REQUIRED: how to get group memberships (pick ONE style)

    # Option A: attribute on user entry
    authorizationQuery:
      attribute: "memberOf"

```
```
# Secret for LDAP bind account (keys: dn, password)
apiVersion: v1
kind: Secret
metadata:
  name: ldap-bind-cred
type: Opaque
stringData:
  dn: "cn=svc_ldap_bind,o
```
```
- name: GET item
  ansible.builtin.uri:
    url: "https://api.example.com/items/123"
    method: GET
    user: "{{ api_user }}"          # username
    password: "{{ api_pass }}"      # password
    force_basic_auth: true          # always send credentials
    validate_certs: no              # like curl -k
    return_content: yes
    status_code: [200, 404]
  register: get_item

- name: Normalize JSON
  ansible.builtin.set_fact:
    item_json: "{{ get_item.json
                   if (get_item.json is defined and get_item.json is mapping)
                   else (get_item.content | default('{}') | from_json) }}"
  when: get_item.status == 200

- name: Create item when bind_dn is missing or empty
  ansible.builtin.uri:
    url: "https://api.example.com/items"
    method: POST
    user: "{{ api_user }}"
    password: "{{ api_pass }}"
    force_basic_auth: true
    validate_certs: no
    headers:
      Content-Type: "application/json"
    body_format: json
    body:
      id: 123
      bind_dn: "cn=service,dc=example,dc=com"
    status_code: [200, 201]
  when:
    - get_item.status == 404
      or item_json.bind_dn is not defined
      or (item_json.bind_dn | trim | length == 0)

```

```

- name: Sleep for 15 seconds before waiting for pods
  ansible.builtin.pause:
    seconds: 15

- name: Wait for all pods to be ready
  ansible.builtin.command: >
    oc wait --for=condition=Ready pods --all
    -n {{ oc_namespace }} --timeout=120s
  register: oc_wait
  changed_when: false
  failed_when: oc_wait.rc != 0


```
```
- name: Fetch secret and render config
  hosts: localhost
  gather_facts: false

  vars:
    secret_name: "my-db-secret"
    secret_namespace: "my-namespace"
    config_template: "templates/app-config.yaml.j2"
    config_output: "/tmp/app-config.yaml"

  tasks:
    - name: Get secret from OpenShift
      ansible.builtin.command: >
        oc get secret {{ secret_name }}
        -n {{ secret_namespace }}
        -o json
      register: oc_secret
      changed_when: false

    - name: Parse secret JSON
      ansible.builtin.set_fact:
        secret_data: "{{ oc_secret.stdout | from_json }}"

    - name: Decode username and password
      ansible.builtin.set_fact:
        db_username: "{{ secret_data.data.username | b64decode }}"
        db_password: "{{ secret_data.data.password | b64decode }}"

    - name: Render config file with secret values
      ansible.builtin.template:
        src: "{{ config_template }}"
        dest: "{{ config_output }}"
        mode: "0600"
      vars:
        db_user: "{{ db_username }}"
        db_pass: "{{ db_password }}"

```

```
oc get secret <secret-name> -n <namespace> -o yaml \
  | python3 -c "import sys,yaml; print(yaml.safe_dump(yaml.safe_load(sys.stdin.read()), sort_keys=False))"

```
```
  - name: Create temporary directory for kubeconfig
      ansible.builtin.tempfile:
        state: directory
        prefix: oc-kubeconfig-
      register: kube_tmpdir

- name: Show temporary kubeconfig directory
  ansible.builtin.debug:
     msg: "Temporary kubeconfig directory is: {{ kube_tmpdir.path }}"

- name: Define kubeconfig path inside temp dir
  ansible.builtin.set_fact:
     kubeconfig_path: "{{ kube_tmpdir.path }}/config"

```

```
usageMeter:
    callHomeClient:
      disabled: true
```
```
openshift-login/
├── group_vars/
│   └── all/
│       ├── vars.yml          # non-secret vars
│       └── vault.yml         # secrets (vault-encrypted)
├── login.yml
```
group_vars/all/vars.yml

```
# OpenShift API endpoint (no trailing slash)
oc_api_url: "https://api.mycluster.example.com:6443"

# User to login as
oc_username: "myuser"

# Optional: project/namespace to switch to after login
oc_project: "my-namespace"

# Where to store kubeconfig for this login
kubeconfig_path: "{{ ansible_env.HOME }}/.kube/oc-login.kubeconfig"

# Set to true if your cluster uses a self-signed cert and you want to skip TLS verify
oc_insecure_skip_tls_verify: false

```

group_vars/all/vault.yml (will be encrypted by Vault)
```
oc_password: "REPLACE_ME"   # will be encrypted; see step 4
```

login.yml
```
- name: Login to OpenShift with oc using a vaulted password
  hosts: localhost
  gather_facts: false

  vars_files:
    - group_vars/all/vars.yml
    - group_vars/all/vault.yml

  pre_tasks:
    - name: Ensure oc CLI is available
      ansible.builtin.command: oc version --client
      register: oc_cli_check
      changed_when: false
      failed_when: oc_cli_check.rc != 0

    - name: Ensure kubeconfig directory exists
      ansible.builtin.file:
        path: "{{ kubeconfig_path | dirname }}"
        state: directory
        mode: "0700"

  tasks:
    - name: Check current oc identity (if already logged in for this kubeconfig)
      ansible.builtin.command: >
        oc whoami --kubeconfig {{ kubeconfig_path }}
      register: oc_whoami
      changed_when: false
      failed_when: false

    - name: Decide if login is needed
      ansible.builtin.set_fact:
        oc_login_needed: "{{ (oc_whoami.rc != 0) or (oc_whoami.stdout | default('') != oc_username) }}"

    - name: oc login (password kept secret)
      ansible.builtin.command: >
        oc login {{ oc_api_url }}
        -u {{ oc_username }}
        -p {{ oc_password }}
        --kubeconfig {{ kubeconfig_path }}
        {% if oc_insecure_skip_tls_verify %} --insecure-skip-tls-verify=true {% endif %}
      no_log: true
      when: oc_login_needed

    - name: Switch to desired project (optional)
      ansible.builtin.command: >
        oc project {{ oc_project }} --kubeconfig {{ kubeconfig_path }}
      when: oc_project is defined and oc_project|length > 0
      register: oc_project_switch
      changed_when: "'now using project' in (oc_project_switch.stdout | lower | default(''))"
```

4) Create the vaulted secrets file

```
ansible-vault encrypt_string 'SuperSecretP@ss!' --name 'oc_password' \
  > group_vars/all/vault.yml

ansible-vault encrypt_string 'SuperSecretP@ss!' --name 'oc_password' \
  > group_vars/all/vault.yml

ansible-playbook login.yml --ask-vault-pass

ansible-playbook login.yml --vault-password-file ~/.vault_pass.txt

```

```
- name: Create a temporary render directory
      ansible.builtin.tempfile:
        state: directory
        prefix: oc-render-
      register: tempdir
- name: Show generated directory
  debug:
    var: tempdir.path

    - name: Set path for rendered manifest
      ansible.builtin.set_fact:
        render_path: "{{ tempdir.path }}/{{ app_name }}.deployment.yaml"

    - name: Render Kubernetes/OpenShift deployment from template
      ansible.builtin.template:
        src: "templates/deployment.yaml.j2"
        dest: "{{ render_path }}"
        mode: "0600"

    - name: Apply rendered manifest with oc
      ansible.builtin.command: >
        oc apply -f {{ render_path }}
        --kubeconfig {{ kubeconfig_path }}
        {% if oc_insecure_skip_tls_verify %} --insecure-skip-tls-verify=true {% endif %}
      register: oc_apply
      changed_when: >
        (' created' in oc_apply.stdout) or
        (' configured' in oc_apply.stdout) or
        ('patched' in oc_apply.stdout)
      failed_when: oc_apply.rc != 0

    - name: Wait for rollout to complete
      ansible.builtin.command: >
        oc rollout status deployment/{{ app_name }}
        --namespace {{ oc_namespace }}
        --kubeconfig {{ kubeconfig_path }}
        --timeout=120s
      register: oc_rollout
      changed_when: false
      failed_when: oc_rollout.rc != 0

  post_tasks:
    - name: Remove temporary render directory
      ansible.builtin.file:
        path: "{{ tempdir.path }}"
        state: absent
```

