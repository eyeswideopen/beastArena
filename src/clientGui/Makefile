
all:
	@(cd sipgen; $(MAKE))
	@(cd siplib; $(MAKE))

install:
	@(cd sipgen; $(MAKE) install)
	@(cd siplib; $(MAKE) install)
	@test -d $(DESTDIR)/Library/Python/2.7/site-packages || mkdir -p $(DESTDIR)/Library/Python/2.7/site-packages
	cp -f sipconfig.py $(DESTDIR)/Library/Python/2.7/site-packages/sipconfig.py
	cp -f /Users/eyeswideopen/Library/Caches/Opera/temporary_downloads/sip-4.13.3/sipdistutils.py $(DESTDIR)/Library/Python/2.7/site-packages/sipdistutils.py

clean:
	@(cd sipgen; $(MAKE) clean)
	@(cd siplib; $(MAKE) clean)
